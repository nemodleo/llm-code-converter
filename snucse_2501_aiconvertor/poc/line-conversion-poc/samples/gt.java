
package am.im.securitiesinqrpritmgmt.service.impl;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import am.im.securitiesinqrpritmgmt.service.SecuritiesInqrPritMgmtBCService;
import custom.cmmn.exception.CgAppUserException;
import custom.cmmn.util.MapDataUtil;
import custom.cmmn.util.UserHeaderUtil;
import com.inswave.elfw.exception.ElException;
import com.inswave.ext.cg.util.CodeUtil;


@Service("securitiesInqrPritMgmtBCServiceImpl")
public class SecuritiesInqrPritMgmtBCServiceImpl implements SecuritiesInqrPritMgmtBCService {

    
    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectInterestRtrvDuda(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0015(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0014(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsBalance(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0005(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsWithdrawal(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0004(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectGnrzReport(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0013(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectCdSalePsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0012(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectBondsSalePsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0011(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectOperatingFundsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0010(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectFundsExecution(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0009(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectExpirationPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0008(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectMmtLedger(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        String trnsDateFrom = null;
        String trnsDateTo = null;
        try {
            
            
            trnsDateFrom = pDoc.getTrnsDateFrom();
            trnsDateTo = pDoc.getTrnsDateTo();
            pDoc.setTrnsDateFrom1(trnsDateFrom);
            pDoc.setTrnsDateTo1(trnsDateTo);
            pDoc.setTrnsDateFrom2(trnsDateFrom);
            pDoc.setTrnsDateTo2(trnsDateTo);
            pDoc.setEstbBankTrnsBrcd1(pDoc.getEstbBankTrnsBrcd());
            pDoc.setEstbBankTrnsBrcd2(pDoc.getEstbBankTrnsBrcd());
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0006(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }
