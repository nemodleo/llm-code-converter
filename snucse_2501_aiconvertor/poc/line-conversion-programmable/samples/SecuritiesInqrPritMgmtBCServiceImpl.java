
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

    
    
    public ArrayList<Map> selectInterestRtrvDuda(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0015(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectDepositsPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0014(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectDepositsBalance(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0005(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectDepositsWithdrawal(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0004(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectGnrzReport(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0013(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectCdSalePsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0012(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectBondsSalePsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0011(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectOperatingFundsPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0010(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectFundsExecution(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0009(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectExpirationPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0008(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectMmtLedger(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        String trnsDateFrom = null;
        String trnsDateTo = null;
        try {
            
            
            trnsDateFrom = MapDataUtil.getString(pDoc, "TRNS_DATE_FROM");
            trnsDateTo = MapDataUtil.getString(pDoc, "TRNS_DATE_TO");
            MapDataUtil.setString(pDoc, "TRNS_DATE_FROM1", trnsDateFrom);
            MapDataUtil.setString(pDoc, "TRNS_DATE_TO1", trnsDateTo);
            MapDataUtil.setString(pDoc, "TRNS_DATE_FROM2", trnsDateFrom);
            MapDataUtil.setString(pDoc, "TRNS_DATE_TO2", trnsDateTo);
            MapDataUtil.setString(pDoc, "ESTB_BANK_TRNS_BRCD1", MapDataUtil.getString(pDoc, "ESTB_BANK_TRNS_BRCD"));
            MapDataUtil.setString(pDoc, "ESTB_BANK_TRNS_BRCD2", MapDataUtil.getString(pDoc, "ESTB_BANK_TRNS_BRCD"));
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0006(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }
